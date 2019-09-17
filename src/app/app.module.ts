import { environment } from '../environments/environment';

// MODULES
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { MaterializeModule } from 'angular2-materialize';
import { AngularFireModule } from 'angularfire2';
import { AngularFireAuthModule } from 'angularfire2/auth';
import { AngularFireDatabaseModule } from 'angularfire2/database';
import { AngularFirestoreModule } from 'angularfire2/firestore';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { ChartsModule } from 'ng2-charts';

// SERVICES
import { DatabaseService } from './services/database.service';
import { AuthService } from './services/auth.service';

// GUARDS
import { AuthGuard } from './guards/auth.guard';

// COMPONENTS
import { AppComponent } from './app.component';
import { ChoosePreviousPicksComponent } from './choose-previous-picks/choose-previous-picks.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { FooterComponent } from './footer/footer.component';
import { GamesComponent } from './games/games.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { MakePicksComponent } from './make-picks/make-picks.component';
import { MenuBarComponent } from './menu-bar/menu-bar.component';
import { PreviousPicksComponent } from './previous-picks/previous-picks.component';
import { SeasonComponent } from './season/season.component';
import { SignupComponent } from './signup/signup.component';
import { ComparePicksComponent } from './compare-picks/compare-picks.component';
import { ChooseComparePicksComponent } from './choose-compare-picks/choose-compare-picks.component';

@NgModule({
  declarations: [
    AppComponent,
    ChoosePreviousPicksComponent,
    DashboardComponent,
    FooterComponent,
    GamesComponent,
    HomeComponent,
    LoginComponent,
    MakePicksComponent,
    MenuBarComponent,
    PreviousPicksComponent,
    SeasonComponent,
    SignupComponent,
    ComparePicksComponent,
    ChooseComparePicksComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFireAuthModule,
    AngularFireDatabaseModule,
    AngularFirestoreModule,
    FormsModule,
    ReactiveFormsModule,
    ChartsModule,
    MaterializeModule
  ],
  providers: [DatabaseService, AuthService, AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
 