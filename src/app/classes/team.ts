export class Team {
    constructor (
        public city: string,
        public name: string,
        public wins: string,
        public losses: string,
        public ties: string,
        public points: number,
        public winner: boolean
    ) { }
}
