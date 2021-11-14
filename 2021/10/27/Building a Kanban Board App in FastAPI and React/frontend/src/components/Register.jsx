import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

function Register(props) {
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();
    const history = useHistory();

    async function createUser() {
        const formData = {
            username: username,
            password_hash: password,
        }

        const response = await fetch('/users', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();

        return data;
    }

    function handleSubmit(e) {
        e.preventDefault();
        
        createUser().then(data => {
            props.setToken(data.access_token);
            localStorage.setItem('token', JSON.stringify(data.access_token));
            history.push("/");
        });
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                Username <input type="text" onChange={e => setUsername(e.target.value)} />
                Password <input type="password" onChange={e => setPassword(e.target.value)} /> 
                <button>Register</button>
            </form>
        </div>
    )
}

export default Register;