import moment from "moment";

export const formatDate = (value?: string | null) => {
    if (!value) return null
    return moment.utc(value).local().format('DD.MM.YYYY HH:mm:ss')
}
