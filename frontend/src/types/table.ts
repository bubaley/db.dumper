export type TableColumn = {
    title: string
    value: string
    class?: string,
    format?: (v: any) => any
}
