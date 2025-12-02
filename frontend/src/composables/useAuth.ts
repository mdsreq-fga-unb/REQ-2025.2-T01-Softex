import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useErrorLogger } from "./useErrorLogger";

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  tipo_funcao:
    | "colaborador"
    | "TI"
    | "Financiro"
    | "Marketing"
    | "Juridíco"
    | "Administrativo"
    | "Projeto";
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const user = ref<User | null>(null);
const accessToken = ref<string | null>(null);
const refreshToken = ref<string | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

const STORAGE_USER = "user";
const STORAGE_ACCESS_TOKEN = "access_token";
const STORAGE_REFRESH_TOKEN = "refresh_token";

const getAuthHeader = (): string | null => {
  if (!accessToken.value) {
    console.warn("⚠️ Token de acesso não encontrado no localStorage");
    return null;
  }
  return `Bearer ${accessToken.value}`;
};

let refreshAccessToken: () => Promise<boolean>; // Declarar antes de authenticatedFetch

const authenticatedFetch = async (
  url: string,
  options: RequestInit = {}
): Promise<Response> => {
  const headers = new Headers(options.headers);
  const authHeader = getAuthHeader();
  if (authHeader) {
    headers.set("Authorization", authHeader);
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 401 && refreshToken.value) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      headers.set("Authorization", `Bearer ${accessToken.value}`);
      return fetch(url, {
        ...options,
        headers,
      });
    }
  }

  return response;
};

const loadUserFromStorage = () => {
  const { logError } = useErrorLogger();

  const storedUser = localStorage.getItem(STORAGE_USER);
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser);
    } catch (e) {
      logError(
        "Falha ao carregar usuário do localStorage",
        { error: e, storedUser },
        "useAuth.loadUserFromStorage",
        e instanceof Error ? e : new Error(String(e))
      );
      localStorage.removeItem(STORAGE_USER);
    }
  }

  accessToken.value = localStorage.getItem(STORAGE_ACCESS_TOKEN);
  refreshToken.value = localStorage.getItem(STORAGE_REFRESH_TOKEN);

  if (accessToken.value) {
    console.log("✅ Token de acesso carregado do localStorage");
  } else {
    console.warn("⚠️ Token de acesso não encontrado no localStorage");
  }

  if (refreshToken.value) {
    console.log("✅ Token de refresh carregado do localStorage");
  } else {
    console.warn("⚠️ Token de refresh não encontrado no localStorage");
  }
};

loadUserFromStorage();

export function useAuth() {
  const router = useRouter();
  const isAuthenticated = computed(() => user.value !== null);

  const logout = () => {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    error.value = null;
    localStorage.removeItem(STORAGE_USER);
    localStorage.removeItem(STORAGE_ACCESS_TOKEN);
    localStorage.removeItem(STORAGE_REFRESH_TOKEN);
    router.push("/login");
  };

  refreshAccessToken = async (): Promise<boolean> => {
    if (!refreshToken.value) {
      logout(); // Se não há refresh token, desloga
      return false;
    }

    try {
      const response = await fetch(`${API_URL}/api/auth/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken.value }),
      });

      if (response.ok) {
        const data = await response.json();
        accessToken.value = data.access;
        localStorage.setItem(STORAGE_ACCESS_TOKEN, data.access);
        return true;
      }
    } catch (e) {
      console.error("Erro ao refresh token:", e);
    }

    logout();
    return false;
  };

  const setTokens = (access: string, refresh: string) => {
    accessToken.value = access;
    refreshToken.value = refresh;
    localStorage.setItem(STORAGE_ACCESS_TOKEN, access);
    localStorage.setItem(STORAGE_REFRESH_TOKEN, refresh);
    console.log("✅ Tokens JWT salvos no localStorage");
  };

  const setUser = (userData: User) => {
    user.value = userData;
    localStorage.setItem(STORAGE_USER, JSON.stringify(userData));
    console.log("✅ Usuário atualizado no estado:", userData);
  };

  const reloadUserFromStorage = () => {
    loadUserFromStorage();
  };

  /**
   * Login via Google SSO
   */
  const googleLogin = async (googleToken: string) => {
    const { logError } = useErrorLogger();
    isLoading.value = true;
    error.value = null;

    try {
      const response = await fetch(`${API_URL}/api/auth/google/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token: googleToken }),
      });

      const data = await response.json();

      if (!response.ok) {
        const errorMsg = data.error || "Erro ao fazer login com Google";
        logError(
          "Falha ao fazer login com Google",
          { status: response.status, data },
          "useAuth.googleLogin"
        );
        throw new Error(errorMsg);
      }

      user.value = data.user;
      localStorage.setItem(STORAGE_USER, JSON.stringify(data.user));
      setTokens(data.access, data.refresh); // Salvar tokens JWT
      router.push("/dashboard");

      return { success: true, isNewUser: data.is_new_user };
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Erro ao fazer login com Google";
      error.value = errorMessage;
      logError(
        "Erro ao fazer login com Google",
        { error: err, googleToken: googleToken ? "presente" : "ausente" },
        "useAuth.googleLogin",
        err instanceof Error ? err : new Error(String(err))
      );
      return { success: false, isNewUser: false };
    } finally {
      isLoading.value = false;
    }
  };

  /**
   * Login tradicional (email/senha)
   */
  const login = async (email: string, password: string) => {
    const { logError } = useErrorLogger();
    isLoading.value = true;
    error.value = null;
    try {
      const response = await fetch(`${API_URL}/api/login/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      let data;
      try {
        data = await response.json();
      } catch (e) {
        // Se não conseguir parsear JSON, tentar ler como texto
        const text = await response.text();
        throw new Error(text || "Erro ao fazer login");
      }

      if (!response.ok) {
        // Tentar extrair mensagem de erro de diferentes formatos do DRF
        let errorMsg = "Email ou senha incorretos";

        if (data.non_field_errors && Array.isArray(data.non_field_errors)) {
          errorMsg = data.non_field_errors[0];
        } else if (data.non_field_errors) {
          errorMsg = data.non_field_errors;
        } else if (data.detail) {
          errorMsg = data.detail;
        } else if (data.error) {
          errorMsg = data.error;
        } else if (data.message) {
          errorMsg = data.message;
        } else if (typeof data === "string") {
          errorMsg = data;
        } else if (data.email && Array.isArray(data.email)) {
          errorMsg = data.email[0];
        } else if (data.password && Array.isArray(data.password)) {
          errorMsg = data.password[0];
        }

        logError(
          "Falha ao fazer login",
          { status: response.status, email, hasPassword: !!password, data },
          "useAuth.login"
        );
        throw new Error(errorMsg);
      }

      // Usar setUser para garantir consistência
      setUser(data.user);
      setTokens(data.access, data.refresh);
      router.push("/dashboard");
      return true;
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Erro ao fazer login";
      error.value = errorMessage;
      logError(
        "Erro ao fazer login",
        { error: err, email },
        "useAuth.login",
        err instanceof Error ? err : new Error(String(err))
      );
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const register = async (userData: {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    password: string;
    tipo_funcao?: string;
  }) => {
    const { logError } = useErrorLogger();
    isLoading.value = true;
    error.value = null;
    try {
      const response = await fetch(`${API_URL}/api/cadastro/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...userData,
          tipo_funcao: userData.tipo_funcao || "colaborador",
        }),
      });
      const data = await response.json();
      if (!response.ok) {
        const errorMsg =
          Object.values(data).flat().join(", ") || "Erro ao criar conta";
        logError(
          "Falha ao cadastrar usuário",
          {
            status: response.status,
            data,
            email: userData.email,
            username: userData.username,
          },
          "useAuth.register"
        );
        throw new Error(errorMsg);
      }
      return await login(userData.email, userData.password);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Erro ao criar conta";
      error.value = errorMessage;
      logError(
        "Erro ao cadastrar usuário",
        { error: err, email: userData.email, username: userData.username },
        "useAuth.register",
        err instanceof Error ? err : new Error(String(err))
      );
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    googleLogin,
    logout,
    register,
    getAuthHeader,
    authenticatedFetch,
    setTokens,
    setUser,
    reloadUserFromStorage,
  };
}
