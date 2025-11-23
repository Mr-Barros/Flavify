// Navbar.tsx

import { Link } from "react-router-dom";

export default function Navbar() {
    const buttonStyle: React.CSSProperties = {
        padding: "8px 14px",
        background: "#333",
        color: "white",
        borderRadius: 6,
        textDecoration: "none",
        marginRight: 10
    };

    return (
        <nav
            style={{
                display: "flex",
                alignItems: "center",
                padding: "15px 20px",
                backgroundColor: "#222",
                marginBottom: 30,
            }}
        >
            <Link to="/" style={buttonStyle}>Questões</Link>
            <Link to="/admin" style={buttonStyle}>Administrador</Link>
        </nav>
    );
}
