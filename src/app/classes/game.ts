import { Team } from "./team";

export class Game {
    constructor (
        public home: Team,
        public away: Team,
        public date: string,
        public time: string,
        public homeImgPath: string,
        public awayImgPath: string
    ) { }
}
