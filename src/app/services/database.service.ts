import { Component } from '@angular/core';
import { Injectable } from '@angular/core';
import { AngularFireDatabase } from 'angularfire2/database';
import { Observable } from 'rxjs';
import { Game } from '../classes/game';
import { Team } from '../classes/team';

@Injectable()
export class DatabaseService {


  constructor(public adb: AngularFireDatabase) { }

  
}
