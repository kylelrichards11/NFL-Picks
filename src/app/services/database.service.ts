import { Injectable } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';
import { Game } from '../classes/game';

@Injectable()
export class DatabaseService {


  constructor(public adb: AngularFireDatabase) { }

  getWeekFromDb(weekNum) {
    let weekArray = new Array();
    let week = this.adb.list<Game>('/2017-2018/' + weekNum).valueChanges();
    week.subscribe(games => {
        games.forEach(game => {
          let uniqueGame = new Game(game.home, game.away, game.date, game.time);
          weekArray.push(uniqueGame);
        })
      });
      console.log(weekArray);
    return weekArray;
  }
}
