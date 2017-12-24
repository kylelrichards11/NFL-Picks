import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from 'angularfire2/auth';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {

  public error: any;

  constructor(public authService: AuthService, private router: Router) { }

  ngOnInit() {
  }

  loginWithEmail(email, password) {
    this.authService.loginWithEmail(email, password).then(() => {
      this.router.navigate(['home']);
      this.authService.authenticated = true;

    }).catch(function (error: any) {
      console.log('ERROR');
      console.log(error.code);
    });
  }

}
