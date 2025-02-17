document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".delete-newsletter").forEach(button => {
        button.addEventListener("click", function () {
            let newsletterId = this.getAttribute("data-id");
            let csrftoken = getCookie("csrftoken");  // Получаем CSRF-токен

            if (confirm("Вы уверены, что хотите удалить эту рассылку?")) {
                fetch(`/newsletter/delete/${newsletterId}/`, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrftoken,
                        "Content-Type": "application/json"
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById(`newsletter-${newsletterId}`).remove();
                        alert("Рассылка удалена!");
                    } else {
                        alert("Ошибка: " + data.error);
                    }
                })
                .catch(error => console.error("Ошибка:", error));
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}