// Set value of cookie and time to expire in days
const setCookie = (cname, cvalue, exdays) => {
    var d = new Date()
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000))
    var expires = `expires=${d.toUTCString()}`
    document.cookie = `${cname}=${cvalue};${expires};path=/;SameSite=Lax`
}

// Get the value of a cookie by name, or empty string if not exists
const getCookie = cname => {
    var name = `${cname}=`
    var ca = document.cookie.split(";")
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i]
        while (c.charAt(0) == " ") {
            c = c.substring(1)
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length)
        }
    }
    return ""
}

export { setCookie, getCookie }
