import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SeasonComponent } from './season/season.component';
import { ChoosePreviousPicksComponent } from './choose-previous-picks/choose-previous-picks.component';
import { PreviousPicksComponent } from './previous-picks/previous-picks.component';
import { MakePicksComponent } from './make-picks/make-picks.component';


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'signup', component: SignupComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [ AuthGuard ] },
  { path: 'season/:seasonId', component: SeasonComponent, canActivate: [ AuthGuard ] },
  { path: 'choosePreviousPicks', component: ChoosePreviousPicksComponent, canActivate: [ AuthGuard ]},
  { path: 'previousPicks/:seasonId/:weekId', component: PreviousPicksComponent, canActivate: [ AuthGuard ]},
  { path: 'makePicks/:seasonId/:weekId', component: MakePicksComponent, canActivate: [ AuthGuard ]}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})

export class AppRoutingModule { }
