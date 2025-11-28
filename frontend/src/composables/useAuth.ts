import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useErrorLogger } from "./useErrorLogger";

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  tipo_permissao: "colaborador" | "lider" | "rh" | "admin";
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const user = ref<User | null>(null);
const isLoading = ref(false);
const error = ref<string | null>(null);

const loadUserFromStorage = () => {
  const { logError } = useErrorLogger();
  const storedUser = localStorage.getItem("user");
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
      localStorage.removeItem("user");
    }
  }
};

loadUserFromStorage();

export function useAuth() {
  const router = useRouter();
  const isAuthenticated = computed(() => user.value !== null);

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

      // Salvar usuário
      user.value = data.user;
      localStorage.setItem("user", JSON.stringify(data.user));
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
      const data = await response.json();
      if (!response.ok) {
        const errorMsg =
          data.error ||
          data.non_field_errors?.[0] ||
          "Email ou senha incorretos";
        logError(
          "Falha ao fazer login",
          { status: response.status, email, hasPassword: !!password, data },
          "useAuth.login"
        );
        throw new Error(errorMsg);
      }

      // Verificar se usuário foi retornado
      if (!data.user) {
        logError(
          "Usuário não encontrado na resposta do login",
          { data },
          "useAuth.login"
        );
        throw new Error("Usuário não encontrado");
      }

      user.value = data.user;
      localStorage.setItem("user", JSON.stringify(data.user));
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

  const logout = () => {
    user.value = null;
    error.value = null;
    localStorage.removeItem("user");
    router.push("/login");
  };

  const register = async (userData: {
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    password: string;
    tipo_permissao?: string;
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
          tipo_permissao: userData.tipo_permissao || "colaborador",
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
  };
}
