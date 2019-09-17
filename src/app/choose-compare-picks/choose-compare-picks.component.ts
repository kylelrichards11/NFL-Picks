import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
 
@Component({
  selector: 'app-choose-compare-picks',
  templateUrl: './choose-compare-picks.component.html',
  styleUrls: ['./choose-compare-picks.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ChooseComparePicksComponent implements OnInit {

    constructor(private router: Router, public authService: AuthService) { }

    seasonId
    weekId
    userId
    otherUserId
  
    ngOnInit() {}

    fixClose() {
      event.stopPropagation()
    }
  
    redirectToPicks(){
      let weekIdArray = this.weekId.split(/(\d+)/)
      let weekNum = weekIdArray[1];
      let path="comparePicks/" + this.seasonId.replace(/\s/g, "") + '/week' + weekNum
      this.router.navigate([path]);
    }

    compareCurrentWeek(){
        let currentSeason = '2019-2020'
        let path="comparePicks/" + currentSeason + "/currentWeek"
        this.router.navigate([path]);
    }

    compareAllTime(){
        let path="compareRecords"
        this.router.navigate([path])
    }

}
