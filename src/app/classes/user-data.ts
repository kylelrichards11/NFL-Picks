export class UserGame {
    constructor (
        public gameId: string,
        public pick: string
    ) { }
}

export class Week {
    constructor ( 
        public weekId: string,
        public games: Array<UserGame>,
        public correct: number,
        public incorrect: number
    ) { }
}

export class Season {
    constructor (
        public years: string,
        public weeks: Array<Week>,
        public correct: number,
        public incorrect: number
    ) { }
}

export class UserData {
    constructor(
        public firstName: string,
        public lastName: string,
        public email: string,
        public correct: number,
        public incorrect: number,
        public seasons: Array<Season>
    ) { }
}
