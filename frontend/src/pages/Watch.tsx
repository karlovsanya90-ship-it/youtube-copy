import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { api } from "../api/client";

export default function Watch() {
    const { id } = useParams();
    const [video, setVideo] = useState<any>(null);
    const [comments, setComments] = useState<any[]>([]);
    const [newComment, setNewComment] = useState("");
    const [likes, setLikes] = useState(0);
    const [isSubscribed, setIsSubscribed] = useState(false);
    const [isAuth, setIsAuth] = useState(false);

    useEffect(() => {
        // Проверяем авторизацию при загрузке
        const token = api.getToken();
        setIsAuth(!!token);

        if (id) {
            api.getVideo(id)
                .then((v) => {
                    setVideo(v);
                    // Запрашиваем статус только если есть токен
                    if (token) {
                        api.getSubStatus(v.channel_id)
                            .then((d) => setIsSubscribed(d.is_subscribed))
                            .catch(() => setIsSubscribed(false));
                    }
                })
                .catch(console.error);

            api.getComments(id).then(setComments).catch(console.error);
            fetch(`http://localhost:8000/api/likes/${id}/likes`)
                .then((r) => r.json())
                .then((d) => setLikes(d.likes_count));
        }
    }, [id]);

    const handleComment = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newComment.trim()) return;
        try {
            const comment = await api.postComment(id!, newComment);
            setComments([comment, ...comments]);
            setNewComment("");
        } catch (err: any) {
            alert(err.message);
        }
    };

    const handleLike = async () => {
        if (!isAuth) return alert("Войдите, чтобы ставить лайки!");
        try {
            await api.likeVideo(id!);
            const res = await fetch(
                `http://localhost:8000/api/likes/${id}/likes`,
            );
            const data = await res.json();
            setLikes(data.likes_count);
        } catch (err) {
            alert("Ошибка!");
        }
    };

    const handleSubscribe = async () => {
        if (!isAuth) return alert("Войдите, чтобы подписаться!");
        if (!video) return;
        try {
            const res = await api.subscribe(video.channel_id);
            setIsSubscribed(res.status === "subscribed");
        } catch (err: any) {
            alert("Ошибка при подписке: " + err.message);
        }
    };

    const handleShare = () => {
        navigator.clipboard.writeText(window.location.href);
        alert("Ссылка на видео скопирована в буфер обмена!");
    };

    if (!video) return <div>Загрузка...</div>;

    return (
        <div
            style={{
                backgroundColor: "#f9f9f9",
                minHeight: "100vh",
                fontFamily: "Roboto, Arial, sans-serif",
            }}
        >
            <header
                style={{
                    padding: "8px 24px",
                    backgroundColor: "white",
                    display: "flex",
                    alignItems: "center",
                    marginBottom: 20,
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
                    maxWidth: 1280,
                    margin: "0 auto",
                    display: "flex",
                    gap: 24,
                    padding: "0 24px",
                }}
            >
                <div style={{ flex: 1 }}>
                    <div
                        style={{
                            backgroundColor: "black",
                            borderRadius: 12,
                            overflow: "hidden",
                            width: "100%",
                            aspectRatio: "16/9",
                        }}
                    >
                        <video
                            controls
                            style={{
                                width: "100%",
                                height: "100%",
                                display: "block",
                            }}
                            src={`http://localhost:8000/api/videos/${id}/stream`}
                        />
                    </div>

                    <h1 style={{ margin: "15px 0 5px 0", fontSize: 20 }}>
                        {video.title}
                    </h1>

                    <div
                        style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center",
                            marginBottom: 20,
                        }}
                    >
                        <div
                            style={{
                                display: "flex",
                                alignItems: "center",
                                gap: 12,
                            }}
                        >
                            <div
                                style={{
                                    width: 40,
                                    height: 40,
                                    borderRadius: "50%",
                                    backgroundColor: "#ccc",
                                }}
                            />
                            <div>
                                <p style={{ margin: 0, fontWeight: 500 }}>
                                    Автор видео
                                </p>
                                <p
                                    style={{
                                        margin: 0,
                                        color: "#606060",
                                        fontSize: 12,
                                    }}
                                >
                                    Канал ID: {video.channel_id.slice(0, 8)}...
                                </p>
                            </div>
                            <button
                                onClick={handleSubscribe}
                                style={{
                                    marginLeft: 20,
                                    padding: "8px 16px",
                                    backgroundColor: isSubscribed
                                        ? "#e5e5e5"
                                        : "#000",
                                    color: isSubscribed ? "#000" : "white",
                                    border: "none",
                                    borderRadius: 18,
                                    cursor: "pointer",
                                    fontWeight: 500,
                                }}
                            >
                                {isSubscribed ? "Отписаться" : "Подписаться"}
                            </button>
                        </div>

                        <div style={{ display: "flex", gap: 10 }}>
                            <button
                                onClick={handleLike}
                                style={{
                                    padding: "8px 16px",
                                    fontSize: 14,
                                    cursor: "pointer",
                                    borderRadius: 18,
                                    border: "none",
                                    backgroundColor: "#e5e5e5",
                                    display: "flex",
                                    alignItems: "center",
                                    gap: 5,
                                    fontWeight: 500,
                                }}
                            >
                                👍 {likes}
                            </button>
                            <button
                                onClick={handleShare}
                                style={{
                                    padding: "8px 16px",
                                    fontSize: 14,
                                    cursor: "pointer",
                                    borderRadius: 18,
                                    border: "none",
                                    backgroundColor: "#e5e5e5",
                                    fontWeight: 500,
                                }}
                            >
                                Поделиться
                            </button>
                        </div>
                    </div>

                    <div
                        style={{
                            backgroundColor: "#e5e5e5",
                            padding: 12,
                            borderRadius: 12,
                            marginBottom: 20,
                            fontSize: 14,
                        }}
                    >
                        <p style={{ margin: 0 }}>{video.description}</p>
                    </div>

                    <h3 style={{ marginTop: 0 }}>
                        {comments.length} комментариев
                    </h3>
                    <form
                        onSubmit={handleComment}
                        style={{
                            display: "flex",
                            gap: 10,
                            marginBottom: 24,
                            alignItems: "center",
                        }}
                    >
                        <div
                            style={{
                                width: 40,
                                height: 40,
                                borderRadius: "50%",
                                backgroundColor: "#ccc",
                                flexShrink: 0,
                            }}
                        />
                        <input
                            type="text"
                            value={newComment}
                            onChange={(e) => setNewComment(e.target.value)}
                            placeholder="Написать комментарий..."
                            style={{
                                flex: 1,
                                padding: 10,
                                border: "none",
                                borderBottom: "1px solid #ccc",
                                outline: "none",
                                backgroundColor: "transparent",
                                fontSize: 14,
                            }}
                        />
                        <button
                            type="submit"
                            style={{
                                padding: "8px 16px",
                                backgroundColor: "#065fd4",
                                color: "white",
                                border: "none",
                                borderRadius: 18,
                                cursor: "pointer",
                                fontWeight: 500,
                            }}
                        >
                            Отправить
                        </button>
                    </form>

                    <div
                        style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: 20,
                        }}
                    >
                        {comments.map((c) => (
                            <div
                                key={c.id}
                                style={{ display: "flex", gap: 12 }}
                            >
                                <div
                                    style={{
                                        width: 40,
                                        height: 40,
                                        borderRadius: "50%",
                                        backgroundColor: "#ccc",
                                        display: "flex",
                                        alignItems: "center",
                                        justifyContent: "center",
                                        fontWeight: "bold",
                                        flexShrink: 0,
                                    }}
                                >
                                    {c.author_name
                                        ? c.author_name[0].toUpperCase()
                                        : "U"}
                                </div>
                                <div>
                                    <p
                                        style={{
                                            margin: "0 0 4px 0",
                                            fontSize: 13,
                                        }}
                                    >
                                        <strong>
                                            {c.author_name || "Пользователь"}
                                        </strong>{" "}
                                        <span
                                            style={{
                                                color: "#606060",
                                                fontSize: 12,
                                            }}
                                        >
                                            {new Date(
                                                c.created_at,
                                            ).toLocaleDateString()}
                                        </span>
                                    </p>
                                    <p style={{ margin: 0, fontSize: 14 }}>
                                        {c.body}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div style={{ width: 400, flexShrink: 0 }}>
                    <p style={{ fontWeight: 500, fontSize: 16, marginTop: 0 }}>
                        Похожие видео
                    </p>
                    {[1, 2, 3, 4].map((i) => (
                        <div
                            key={i}
                            style={{
                                display: "flex",
                                gap: 10,
                                marginBottom: 12,
                                cursor: "pointer",
                            }}
                        >
                            <div
                                style={{
                                    width: 168,
                                    height: 94,
                                    backgroundColor: "#333",
                                    borderRadius: 8,
                                    flexShrink: 0,
                                }}
                            />
                            <div>
                                <h4
                                    style={{
                                        margin: "0 0 4px 0",
                                        fontSize: 14,
                                        fontWeight: 500,
                                        lineHeight: 1.4,
                                    }}
                                >
                                    Заголовок видео #{i}
                                </h4>
                                <p
                                    style={{
                                        margin: 0,
                                        color: "#606060",
                                        fontSize: 12,
                                    }}
                                >
                                    Название канала
                                </p>
                                <p
                                    style={{
                                        margin: 0,
                                        color: "#606060",
                                        fontSize: 12,
                                    }}
                                >
                                    10 тыс. просмотров
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
}
