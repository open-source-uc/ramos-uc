export class Module {
    constructor(type, days, mods, room) {
        this.type = type
        this.days = days
        this.mods = mods
        this.room = room
    }

    static moduleFromString(str) {
        try {
            const [data, type, room] = str.split("<>")
            const [days, mods] = data.split(":")
            return new Module(type,
                days.split("-").sort(),
                mods.split(",").map(Number).sort(),
                room)
        } catch (e) {
            return null
        }
    }

    static scheduleFromString(str) {
        return str.split("ROW: ").map(Module.moduleFromString).filter(Boolean)
    }

    static equals(a, b) {
        if (a.type != b.type) return false
        // Days
        if (a.days.length != b.days.length) return false
        for (let i = 0; i < a.days.length; i++){
            if (a.days[i] != b.days[i]) return false
        }
        // Modules
        if (a.mods.length != b.mods.length) return false
        for (let i = 0; i < a.mods.length; i++){
            if (a.mods[i] != b.mods[i]) return false
        }

        return true
    }

    static equalSchedules(a, b) {
        if (a.length != b.length) return false
        return a.every(m => b.some(m2 => this.equals(m, m2)))
    }

    static compatible(a, b) {
        return a.days.every(d => b.days.every(d2 => d != d2)) || a.mods.every(m => b.mods.every(m2 => m != m2))
    }

    static compatibleSchedules(a, b) {
        return a.every(m => b.every(m2 => this.compatible(m, m2)))
    }
}
