import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/client";

export default function Upload() {
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!file) return alert("Выберите файл");
        setLoading(true);

        const formData = new FormData();
        formData.append("title", title);
        formData.append("description", description);
        formData.append("file", file);

        try {
            const token = api.getToken();
            if (!token) {
                alert("Сначала войдите в аккаунт!");
                navigate("/login");
                return;
            }

            const res = await fetch("http://localhost:8000/api/videos/upload", {
                method: "POST",
                headers: { Authorization: `Bearer ${token}` },
                body: formData,
            });

            if (!res.ok) throw new Error("Ошибка загрузки");
            const data = await res.json();
            alert("Видео успешно загружено!");
            navigate(`/watch/${data.id}`);
        } catch (err: any) {
            alert(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            style={{
                fontFamily: "Roboto, Arial, sans-serif",
                backgroundColor: "#f9f9f9",
                minHeight: "100vh",
            }}
        >
            <header
                style={{
                    padding: "8px 24px",
                    backgroundColor: "white",
                    display: "flex",
                    alignItems: "center",
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
                        }}
                    >
                        YouTube Copy
                    </h1>
                </Link>
            </header>

            <main
                style={{
                    maxWidth: 800,
                    margin: "40px auto",
                    backgroundColor: "white",
                    padding: 40,
                    borderRadius: 8,
                    boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
                }}
            >
                <h2 style={{ marginTop: 0, fontSize: 24 }}>Загрузка видео</h2>
                <form
                    onSubmit={handleSubmit}
                    style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 20,
                    }}
                >
                    <div
                        style={{
                            border: "2px dashed #ccc",
                            borderRadius: 8,
                            padding: 40,
                            textAlign: "center",
                            backgroundColor: "#fafafa",
                        }}
                    >
                        <input
                            type="file"
                            accept="video/*"
                            onChange={(e) =>
                                setFile(e.target.files?.[0] || null)
                            }
                            required
                            style={{ fontSize: 16 }}
                        />
                    </div>

                    <input
                        type="text"
                        placeholder="Название видео (обязательно)"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        required
                        style={{
                            padding: 12,
                            fontSize: 16,
                            border: "1px solid #ccc",
                            borderRadius: 4,
                            outline: "none",
                        }}
                    />
                    <textarea
                        placeholder="Описание"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        style={{
                            padding: 12,
                            fontSize: 16,
                            minHeight: 120,
                            border: "1px solid #ccc",
                            borderRadius: 4,
                            outline: "none",
                            resize: "vertical",
                        }}
                    />

                    <div
                        style={{
                            display: "flex",
                            justifyContent: "flex-end",
                            gap: 15,
                        }}
                    >
                        <Link
                            to="/"
                            style={{
                                padding: "10px 20px",
                                textDecoration: "none",
                                color: "#606060",
                                fontWeight: 500,
                            }}
                        >
                            Отмена
                        </Link>
                        <button
                            type="submit"
                            disabled={loading}
                            style={{
                                padding: "10px 20px",
                                fontSize: 16,
                                backgroundColor: "#065fd4",
                                color: "white",
                                border: "none",
                                borderRadius: 4,
                                cursor: "pointer",
                                fontWeight: 500,
                            }}
                        >
                            {loading ? "Загрузка..." : "Загрузить"}
                        </button>
                    </div>
                </form>
            </main>
        </div>
    );
}
