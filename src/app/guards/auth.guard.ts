import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { AngularFireAuth } from 'angularfire2/auth';
import { Observable, from } from 'rxjs';
import { take, map, tap } from 'rxjs/operators'

@Injectable()
export class AuthGuard implements CanActivate {

  constructor(private router: Router, private authService: AuthService, private afAuth: AngularFireAuth) { }

  private sub: any = null;

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
    return from(this.afAuth.authState)
    .pipe(take(1))
    .pipe(map(user => !!user))
    .pipe(tap(authenticated => {
      if (!authenticated) {
        this.router.navigate(['signup']);
      }
    }));
  }
}
