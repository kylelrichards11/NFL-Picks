import { environment } from '../environments/environment';

//NG2-MATERIALIZE MODULES
import { MzSelectModule, MzSelectDirective } from 'ng2-materialize';
import { MzValidationModule } from 'ng2-materialize';

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
import { HomeComponent } from './home/home.component';
import { MenuBarComponent } from './menu-bar/menu-bar.component';
import { FooterComponent } from './footer/footer.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { GamesComponent } from './games/games.component';
import { SeasonComponent } from './season/season.component';
import { PreviousPicksComponent } from './previous-picks/previous-picks.component';
import { ChoosePreviousPicksComponent } from './choose-previous-picks/choose-previous-picks.component';
import { MakePicksComponent } from './make-picks/make-picks.component';


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    MenuBarComponent,
    FooterComponent,
    LoginComponent,
    SignupComponent,
    DashboardComponent,
    GamesComponent,
    SeasonComponent,
    PreviousPicksComponent,
    ChoosePreviousPicksComponent,
    MakePicksComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFireAuthModule,
    AngularFireDatabaseModule,
    AngularFirestoreModule,
    FormsModule,
    MzSelectModule,
    ReactiveFormsModule,
    MzValidationModule,
    ChartsModule
  ],
  providers: [DatabaseService, AuthService, AuthGuard],
  bootstrap: [AppComponent]
})
export class AppModule { }
