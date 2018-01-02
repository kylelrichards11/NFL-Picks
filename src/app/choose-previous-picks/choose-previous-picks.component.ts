import { Component, OnInit } from '@angular/core';
import { MzSelectModule } from 'ng2-materialize'
import { Router } from '@angular/router';

@Component({
  selector: 'app-choose-previous-picks',
  templateUrl: './choose-previous-picks.component.html',
  styleUrls: ['./choose-previous-picks.component.css']
})
export class ChoosePreviousPicksComponent implements OnInit {

  constructor(private router: Router) { }

  seasonId
  weekId

  ngOnInit() {
  }

  redirectToPicks(){
    let weekIdArray = this.weekId.split(/(\d+)/)
    let weekNum = weekIdArray[1];
    let path="previousPicks/" + this.seasonId + '/week' + weekNum
    this.router.navigate([path]);
  }
}

