import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/client";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const data = await api.login({ email, password });
            api.setToken(data.access_token);
            navigate("/");
        } catch (err: any) {
            setError(err.message);
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
            <h2>Вход</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
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
                    placeholder="Пароль"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
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
                    Войти
                </button>
            </form>
            <p style={{ marginTop: 15, textAlign: "center" }}>
                Нет аккаунта?{" "}
                <Link to="/register" style={{ color: "blue" }}>
                    Зарегистрироваться
                </Link>
            </p>
        </div>
    );
}
