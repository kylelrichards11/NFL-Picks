import { Component, OnInit } from '@angular/core';
import { DatabaseService } from '../services/database.service';
import { DatabaseReference } from 'angularfire2/database/interfaces';
import { AngularFireDatabase } from 'angularfire2/database';
import { Game } from '../classes/game';
import { Team } from '../classes/team';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  gameArray = new Array();
  weekNum = 'week16';

  constructor(public dbSrv: DatabaseService, public adb: AngularFireDatabase) { }

  ngOnInit() {

    this.adb.list<Game>('/2017-2018/' + this.weekNum).valueChanges().subscribe(games => {
      this.gameArray = [];
      games.forEach(game => {

        //get home and away team name without city for image name
        var homeImgPath = "../assets/teamLogos/" + game.home.name.toLowerCase() + ".png"
        var awayImgPath = "../assets/teamLogos/" + game.away.name.toLowerCase() + ".png"

        let uniqueGame = new Game(game.home, game.away, game.date, game.time, homeImgPath, awayImgPath);
        this.gameArray.push(uniqueGame);
      })
    });


  }
}
