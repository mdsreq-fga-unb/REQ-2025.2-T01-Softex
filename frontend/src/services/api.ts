import axios from "axios";

// 1. Cria a instância
const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// 2. Adiciona o Interceptor (CRUCIAL para o Django aceitar a requisição)
// Isso injeta o cabeçalho "Authorization: Bearer <token>" em tudo
api.interceptors.request.use(
  (config) => {
    // Verifique se você salvou como 'access_token', 'token' ou 'jwt' no login
    const token =
      localStorage.getItem("access_token") || localStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 3. Exportação PADRÃO (Resolve o erro "does not provide an export named default")
export default api;
