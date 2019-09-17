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
  correctPicksByWeekButtonText = 'Show Average'
  showTrend = false;

  public picksByWeekBarChartOptions: any = {
    scaleShowVerticalLines: false,
    responsive: true,
    scales: {
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Correct Picks',
          fontSize: 16,
          max: 16
        },
        ticks: {
          beginAtZero: true,
          max: 16
        }
      }],
      xAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Week            ', //spaces temporary fix to center this on the graph instead of x-axis
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
    { data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: '2014-2015' },
    { data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: '2015-2016' },
    { data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: '2016-2017' },
    { data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: '2017-2018' }
  ];

  picksByWeekBarChartTrendData: any[] = [{ data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], label: 'Trend by Week' }]

  ngOnInit() {
    this.authService.getUserId().subscribe(user_id => {
      this.userId = user_id; //Get the User Id
      this.adb.object<any>('/users/' + this.userId).valueChanges().subscribe(user => {  //subscribe to the user
        this.userHistory = user;
        this.percentCorrect = ((Number(user.correct)/(Number(user.correct) + Number(user.incorrect))) * 100).toFixed(2);
      });

      var allSeasonData: any[] = []; //an array that holds the data for all seasons that the bar graph will display
      var allTrendData: any[] = []; //an array that holds the data for the trend of data by week that the bar graph will display
      let seasonIdsArray = ['2014-2015', '2015-2016', '2016-2017', '2017-2018']; //an array of ids for each season
      let numberOfSeasons = seasonIdsArray.length

      //an array that will hold the data for each week across all seasons
      var trendDataArray = new Array(17);
      for (var i = 0; i < 17; i++) { 
        trendDataArray[Number(i)] = 0; //initialize the array to have 0
      }

      //loop through each season
      for (let i in seasonIdsArray) {

        //subscribe to the season
        this.adb.list<Week>('/users/' + this.userId + '/seasons/' + seasonIdsArray[Number(i)] + '/weeks').valueChanges().subscribe(weeks => {

          var seasonDataArray = new Array(17); //an array to hold the data for each week of this season

          weeks.forEach(week => { //iterate through weeks
            let weekNum = week.weekId.split(/(\d+)/); //get the number of the week from the week id
            seasonDataArray[Number(weekNum[1]) - 1] = week.correct; //store the number of the correct picks in the correct spot in the seasonDataArray (weekNum - 1)
            trendDataArray[Number(weekNum[1]) - 1] += week.correct; //add the number of correct picks for that week across all seasons
          });

          //push the season's data to the array for all seasons
          allSeasonData.push({ data: seasonDataArray, label: seasonIdsArray[Number(i)] });

          //if this is the last season, save all season data to the barChartData array
          if (Number(i) === numberOfSeasons - 1) {
            this.picksByWeekBarChartData = allSeasonData;

            //get trend data by finding average of all weeks
            for (let j in trendDataArray) {
              trendDataArray[Number(j)] = Number((trendDataArray[Number(j)] / numberOfSeasons).toFixed(2));
            }
            console.log('filled in array', trendDataArray)
            allTrendData.push({ data: trendDataArray, label: 'Average by Week'}); //push the data to an empty array
            this.picksByWeekBarChartTrendData = allTrendData; //set the trend data class variable to this array
            //NOTE: The only reason I did the last two steps is because that this the way I did it for the season data, which works
          }
        });
      }
    });
  }

  correctPicksByWeekButtonClicked() {
    if(this.showTrend) {
      this.correctPicksByWeekButtonText = 'Show Average';
      this.showTrend = false;
    }
    else {
      this.correctPicksByWeekButtonText = 'Show Each Season';
      this.showTrend = true;
    }
  }
}
