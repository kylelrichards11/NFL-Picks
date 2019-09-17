import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { AngularFireDatabase } from 'angularfire2/database';

@Component({
  selector: 'app-compare-records',
  templateUrl: './compare-records.component.html',
  styleUrls: ['./compare-records.component.scss']
})
export class CompareRecordsComponent implements OnInit {

  constructor(public adb: AngularFireDatabase, public authService: AuthService) { }

  userId
  otherUserId
  otherUserName
  showRecords = false
  userData
  otherUserData
  seasonRecords = []

  ngOnInit() {
    this.authService.getUserId().subscribe(user_id => {
        this.userId = user_id;

        if(this.userId == "H3EI5DDrbldJEg2FxEk6N9oYnaf2") {
            this.otherUserId = "wzht1HEeVZdTSw61qM6jS2j7TqN2"
            this.otherUserName = "Jay"
        }
        else {
            this.otherUserId = "H3EI5DDrbldJEg2FxEk6N9oYnaf2"
            this.otherUserName = "Kyle"
        }

        this.adb.object<any>('/users/' + this.userId).valueChanges().subscribe(user => {
            this.userData = user
            var seasons = user.seasons
            for (let season in seasons) {
                let record = String(seasons[season]["correct"]) + " - " + String(seasons[season]["incorrect"])
                this.seasonRecords.push([season, record])
            }
        })

        this.adb.object<any>('/users/' + this.otherUserId).valueChanges().subscribe(otherUser => {
            this.otherUserData = otherUser
            var seasons = otherUser.seasons
            var i = 0
            for (let season in seasons) {
                let record = String(seasons[season]["correct"]) + " - " + String(seasons[season]["incorrect"])
                this.seasonRecords[i].push(record)
                i++
            }
        })

        

        this.showRecords = true;
        });
  }

}
