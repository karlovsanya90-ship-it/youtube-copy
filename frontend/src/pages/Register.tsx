import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/client";

export default function Register() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [channelName, setChannelName] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        try {
            await api.register({ email, password, channel_name: channelName });
            const loginData = await api.login({ email, password });
            api.setToken(loginData.access_token);
            navigate("/");
        } catch (err: any) {
            setError(err.message); // Теперь здесь будет понятный текст
        }
    };

    return (
        <div
            style={{
                padding: 20,
                fontFamily: "Arial",
                maxWidth: 400,
                margin: "50px auto",
                border: "1px solid #ccc",
                borderRadius: 8,
            }}
        >
            <h2>Регистрация</h2>
            {error && (
                <p style={{ color: "red", fontWeight: "bold" }}>{error}</p>
            )}
            <form
                onSubmit={handleSubmit}
                style={{ display: "flex", flexDirection: "column", gap: 10 }}
            >
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    style={{ padding: 10 }}
                />
                <input
                    type="password"
                    placeholder="Пароль (минимум 8 символов)"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    style={{ padding: 10 }}
                />
                <input
                    type="text"
                    placeholder="Название канала"
                    value={channelName}
                    onChange={(e) => setChannelName(e.target.value)}
                    required
                    style={{ padding: 10 }}
                />
                <button
                    type="submit"
                    style={{
                        padding: 10,
                        backgroundColor: "#ff0000",
                        color: "white",
                        border: "none",
                        cursor: "pointer",
                    }}
                >
                    Создать аккаунт
                </button>
            </form>
            <p style={{ marginTop: 15, textAlign: "center" }}>
                Уже есть аккаунт?{" "}
                <Link to="/login" style={{ color: "blue" }}>
                    Войти
                </Link>
            </p>
        </div>
    );
}
