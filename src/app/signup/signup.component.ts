import { Component } from '@angular/core';
import { User } from '../classes/user';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {

  model = new User('', '', '', '', '', false);

  constructor(public authService: AuthService, private router: Router) { }
  onSubmit() { }

  registerDonor() {
    if (this.model.password === this.model.confirmPassword) {
      this.authService.registerUser(this.model).then(() => {
        this.router.navigate(['home']);
        console.log('Successful sign up');
      });
    } else {
      document.getElementById('passNotMatch').innerHTML = 'Passwords did not match. Try Again.';
    }
  }

}
