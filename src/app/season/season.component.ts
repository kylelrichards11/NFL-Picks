import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-season',
  templateUrl: './season.component.html',
  styleUrls: ['./season.component.css']
})
export class SeasonComponent implements OnInit {

  constructor(private activatedRoute: ActivatedRoute) { }

  seasonId

  ngOnInit() {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.seasonId = params['seasonId'];
    });

    console.log(this.seasonId);
  }

}
