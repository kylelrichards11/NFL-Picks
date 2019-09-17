import { AngularFireAuth } from 'angularfire2/auth';
import { AngularFireDatabase } from 'angularfire2/database';
import { Injectable } from '@angular/core';
import { Observable, from } from 'rxjs';
import { take, map, tap } from 'rxjs/operators'

@Injectable()
export class AuthService {

  public authenticated;

  constructor(public afAuth: AngularFireAuth, public db: AngularFireDatabase) {
  }

  public getUserId() {
    return from(this.afAuth.authState)
      .pipe(take(1))
      .pipe(map(user => user.uid));
  }

  public isAuthenticated() {
    if (this.authenticated === undefined) {
      let state = this.checkAuth();
      state.then(auth => {
        this.authenticated = auth;
      });
    }
    return this.authenticated;
  }

  public checkAuth() {
    return from(this.afAuth.authState)
      .pipe(take(1))
      .pipe(map(user => !!user))
      .toPromise();
  }

  registerUser(user) {
    return this.afAuth.auth.createUserWithEmailAndPassword(
      user.email,
      user.password
    ).then((saved_user) => {
      this.saveUserToDb(saved_user.user.uid, user);
    });
  }

  saveUserToDb(uid, user) {
    console.log("user = ", user);
    console.log("user id = ", uid);
    return this.db.object('users/' + uid).set({
      first_name: user.firstName,
      last_name: user.lastName,
      email: user.email
    });
  }

  loginWithEmail(email, password) {
    this.authenticated = true;
    return this.afAuth.auth.signInWithEmailAndPassword(email, password);
  }

  subscribe(onNext: (value: any) => void, onThrow?: (exception: any) => void, onReturn?: () => void) {
    return this.afAuth.authState.subscribe();
  }

  logOut() {
    this.authenticated = false;
    this.afAuth.auth.signOut();
  }

}


