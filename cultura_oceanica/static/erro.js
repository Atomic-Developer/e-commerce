$cruCallback('handleResponse', ({ status, data }, form) => {
    const erroMsgDiv = document.getElementById("erro-msg");

    if (status === 400 && erroMsgDiv) {
        erroMsgDiv.classList.remove("d-none"); 
        erroMsgDiv.textContent = data.error || "este email ja se encontra cadastrado";
    } else if (status === 200) {
        erroMsgDiv?.classList.add("d-none");
        window.location.href ="/";
    }
    });
    document.getElementById("erro-msg")



$cruCallback('handleLogin', ({ status, data }, form) => {
    if (status === 200) {
        alert(`Bem-vindo, ${data.nome}`);

        if (data.nome === 'Admin') {
            window.location.href = '/criar_produto';
        } else {
            window.location.href = '/';
        }
    } else if (status === 401) {
        document.getElementById("erro-msg").classList.remove("d-none");
        document.getElementById("erro-msg").innerText = data.error || "Erro ao fazer login.";
    }
});

