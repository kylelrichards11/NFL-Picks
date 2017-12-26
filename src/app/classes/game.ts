import { Team } from "./team";

export class Game {
    constructor (
        public home: Team,
        public away: Team,
        public gameId: string,
        public date: string,
        public time: string,
        public started: boolean,
        public homeImgPath: string,
        public awayImgPath: string
    ) { }
}
