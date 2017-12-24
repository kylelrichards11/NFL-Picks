import { Component, OnInit, Input } from '@angular/core';
import { DatabaseReference } from 'angularfire2/database/interfaces';
import { AngularFireDatabase } from 'angularfire2/database';
import { Game } from '../classes/game';

@Component({
  selector: 'app-games',
  templateUrl: './games.component.html',
  styleUrls: ['./games.component.css']
})
export class GamesComponent implements OnInit {

  @Input() weekId: string;

  gameArray = new Array();

  constructor(public adb: AngularFireDatabase) { }

  ngOnInit() {

    this.adb.list<Game>('/2017-2018/' + this.weekId).valueChanges().subscribe(games => {
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
