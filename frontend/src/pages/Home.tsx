import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function Home() {
    const [videos, setVideos] = useState<any[]>([]);
    const [isAuth, setIsAuth] = useState(false);

    useEffect(() => {
        api.getVideos().then(setVideos).catch(console.error);
        setIsAuth(!!api.getToken());
    }, []);

    const handleLogout = () => {
        api.logout();
        window.location.reload();
    };

    return (
        <div
            style={{
                fontFamily: "Roboto, Arial, sans-serif",
                backgroundColor: "#f9f9f9",
                minHeight: "100vh",
            }}
        >
            {/* Шапка сайта */}
            <header
                style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "8px 24px",
                    backgroundColor: "white",
                    position: "sticky",
                    top: 0,
                    zIndex: 10,
                }}
            >
                <Link
                    to="/"
                    style={{
                        textDecoration: "none",
                        display: "flex",
                        alignItems: "center",
                        gap: 5,
                    }}
                >
                    <span style={{ fontSize: 24 }}>▶</span>
                    <h1
                        style={{
                            margin: 0,
                            color: "#000",
                            fontSize: 20,
                            fontWeight: "bold",
                            letterSpacing: -1,
                        }}
                    >
                        YouTube Copy
                    </h1>
                </Link>
                <div style={{ display: "flex", gap: 15, alignItems: "center" }}>
                    <Link
                        to="/upload"
                        style={{
                            textDecoration: "none",
                            color: "#065fd4",
                            fontWeight: 500,
                            fontSize: 14,
                        }}
                    >
                        Создать
                    </Link>
                    {isAuth ? (
                        <button
                            onClick={handleLogout}
                            style={{
                                background: "none",
                                border: "1px solid #ccc",
                                borderRadius: 18,
                                padding: "6px 16px",
                                cursor: "pointer",
                                fontWeight: 500,
                            }}
                        >
                            Выйти
                        </button>
                    ) : (
                        <>
                            <Link
                                to="/login"
                                style={{
                                    textDecoration: "none",
                                    color: "#065fd4",
                                    fontWeight: 500,
                                    fontSize: 14,
                                }}
                            >
                                Войти
                            </Link>
                            <Link
                                to="/register"
                                style={{
                                    textDecoration: "none",
                                    color: "#065fd4",
                                    fontWeight: 500,
                                    fontSize: 14,
                                }}
                            >
                                Регистрация
                            </Link>
                        </>
                    )}
                </div>
            </header>

            {/* Сетка видео */}
            <main style={{ padding: "24px 40px" }}>
                <div
                    style={{
                        display: "grid",
                        gridTemplateColumns:
                            "repeat(auto-fill, minmax(280px, 1fr))",
                        gap: 24,
                    }}
                >
                    {videos.map((video) => (
                        <Link
                            to={`/watch/${video.id}`}
                            key={video.id}
                            style={{ textDecoration: "none", color: "black" }}
                        >
                            <div
                                style={{
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: 10,
                                }}
                            >
                                <div
                                    style={{
                                        position: "relative",
                                        width: "100%",
                                        aspectRatio: "16/9",
                                        backgroundColor: "#000",
                                        borderRadius: 8,
                                        overflow: "hidden",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                    }}
                                >
                                    <span
                                        style={{
                                            color: "white",
                                            fontSize: 40,
                                            opacity: 0.5,
                                        }}
                                    >
                                        ▶
                                    </span>
                                    <div
                                        style={{
                                            position: "absolute",
                                            bottom: 8,
                                            right: 8,
                                            backgroundColor: "rgba(0,0,0,0.8)",
                                            color: "white",
                                            padding: "2px 4px",
                                            borderRadius: 4,
                                            fontSize: 12,
                                        }}
                                    >
                                        0:05
                                    </div>
                                </div>
                                <div style={{ display: "flex", gap: 12 }}>
                                    <div
                                        style={{
                                            width: 36,
                                            height: 36,
                                            borderRadius: "50%",
                                            backgroundColor: "#ccc",
                                            flexShrink: 0,
                                        }}
                                    />
                                    <div>
                                        <h3
                                            style={{
                                                margin: "0 0 4px 0",
                                                fontSize: 16,
                                                fontWeight: 500,
                                                lineHeight: 1.4,
                                                display: "-webkit-box",
                                                WebkitLineClamp: 2,
                                                WebkitBoxOrient: "vertical",
                                                overflow: "hidden",
                                            }}
                                        >
                                            {video.title}
                                        </h3>
                                        <p
                                            style={{
                                                margin: 0,
                                                color: "#606060",
                                                fontSize: 14,
                                            }}
                                        >
                                            Канал ID:{" "}
                                            {video.channel_id.slice(0, 8)}...
                                        </p>
                                        <p
                                            style={{
                                                margin: 0,
                                                color: "#606060",
                                                fontSize: 14,
                                            }}
                                        >
                                            0 просмотров • сейчас
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
                {videos.length === 0 && (
                    <p
                        style={{
                            textAlign: "center",
                            marginTop: 50,
                            color: "#606060",
                        }}
                    >
                        Пока нет видео. Загрузите первое!
                    </p>
                )}
            </main>
        </div>
    );
}
