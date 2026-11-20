const API_URL = "http://localhost:8000/api";

export const api = {
    getToken: () => localStorage.getItem("token"),
    setToken: (token: string) => localStorage.setItem("token", token),
    logout: () => localStorage.removeItem("token"),

    async request(endpoint: string, options: RequestInit = {}) {
        const token = this.getToken();
        const headers: HeadersInit = { ...options.headers };

        if (token) {
            (headers as Record<string, string>)["Authorization"] =
                `Bearer ${token}`;
        }

        if (options.body && !(options.body instanceof FormData)) {
            (headers as Record<string, string>)["Content-Type"] =
                "application/json";
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers,
        });

        if (!response.ok) {
            const errorData = await response.json();
            if (Array.isArray(errorData.detail)) {
                throw new Error(errorData.detail[0].msg);
            }
            throw new Error(errorData.detail || "Ошибка запроса");
        }
        return response.json();
    },

    login: (data: any) =>
        api.request("/auth/login", {
            method: "POST",
            body: JSON.stringify(data),
        }),
    register: (data: any) =>
        api.request("/auth/register", {
            method: "POST",
            body: JSON.stringify(data),
        }),
    getVideos: () => api.request("/videos/"),
    getVideo: (id: string) => api.request(`/videos/${id}`),
    getComments: (id: string) => api.request(`/comments/video/${id}`),
    postComment: (id: string, body: string) =>
        api.request(`/comments/video/${id}`, {
            method: "POST",
            body: JSON.stringify({ body }),
        }),
    likeVideo: (id: string) =>
        api.request(`/likes/${id}/like`, { method: "POST" }),

    // --- ДОБАВИЛИ МЕТОДЫ ДЛЯ ПОДПИСКИ ---
    subscribe: (channelId: string) =>
        api.request(`/subscriptions/${channelId}`, { method: "POST" }),
    getSubStatus: (channelId: string) =>
        api.request(`/subscriptions/${channelId}/status`),
};
