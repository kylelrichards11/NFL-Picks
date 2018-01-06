import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { AngularFireDatabase } from 'angularfire2/database';
import { UserData, Season, Week, UserGame } from '../classes/user-data';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  constructor(public authService: AuthService, public adb: AngularFireDatabase) { }

  userId;
  userHistory;
  percentCorrect = '0';

  public picksByWeekBarChartOptions: any = {
    scaleShowVerticalLines: false,
    responsive: true,
    scales: {
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Correct Picks',
          fontSize: 16
        },
        ticks: {
          beginAtZero: true
        }
      }],
      xAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Week',
          fontSize: 16
        },
      }]
    },
    title: {
      display: true,
      text: 'Correct Picks by Week',
      fontSize: 36
    }

  };
  public picksByWeekBarChartLabels: string[] = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Week 11', 'Week 12', 'Week 13', 'Week 14', 'Week 15', 'Week 16', 'Week 17'];
  public picksByWeekBarChartType: string = 'bar';
  public picksByWeekBarChartLegend: boolean = true;

  // This is the data for the bar graph to display before the data from firebase comes in
  public picksByWeekBarChartData: any[] = [
    { data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: '2015-2016' },
    { data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: '2016-2017' },
    { data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: '2017-2018' }
  ];

  ngOnInit() {
    this.authService.getUserId().subscribe(user_id => {
      this.userId = user_id; //Get the User Id
      this.adb.object<any>('/users/' + this.userId).valueChanges().subscribe(user => {  //subscribe to the user
        this.userHistory = user;
        this.percentCorrect = ((Number(user.correct)/(Number(user.correct) + Number(user.incorrect))) * 100).toFixed(2);
        console.log(this.percentCorrect)
      });

      var allData: any[] = []; //an array that holds the data that the bar graph will display
      let seasonIdsArray = ['2015-2016', '2016-2017', '2017-2018']; //an array of ids for each season
      let seasonNumber = seasonIdsArray.length

      //loop through each season
      for (let i in seasonIdsArray) {

        //subscribe to the season
        this.adb.list<Week>('/users/' + this.userId + '/seasons/' + seasonIdsArray[Number(i)] + '/weeks').valueChanges().subscribe(weeks => {

          var seasonDataArray = new Array(17); //an array to hold the data for each week

          weeks.forEach(week => { //iterate through weeks
            let weekNum = week.weekId.split(/(\d+)/) //get the number of the week from the week id
            seasonDataArray[Number(weekNum[1]) - 1] = week.correct //store the number of the correct picks in the correct spot in the seasonDataArray (weekNum - 1)
          });

          //push the season's data to the array for all seasons
          allData.push({ data: seasonDataArray, label: seasonIdsArray[Number(i)] });

          //if this is the last season, save all season data to the barChartData array
          if (Number(i) === seasonNumber - 1) {
            this.picksByWeekBarChartData = allData;
          }
        });
      }
    });
  }
}
