// Set value of cookie and time to expire in days
const setCookie = (cname, cvalue, exdays) => {
    var expire_date = new Date()
    expire_date.setTime(expire_date.getTime() + (exdays * 24 * 60 * 60 * 1000))
    var expires = `expires=${expire_date.toUTCString()}`
    document.cookie = `${cname}=${cvalue};${expires};path=/;SameSite=Lax`
}

// Get the value of a cookie by name, or empty string if not exists
const getCookie = cname => {
    const cookie_regrex = `${cname}=(?<value>[^;]*?);`
    const match = document.cookie.match(cookie_regrex)
    return match ? match.groups.value : ""
}

export { setCookie, getCookie }
