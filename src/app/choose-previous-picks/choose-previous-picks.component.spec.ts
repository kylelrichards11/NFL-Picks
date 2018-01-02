import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChoosePreviousPicksComponent } from './choose-previous-picks.component';

describe('ChoosePreviousPicksComponent', () => {
  let component: ChoosePreviousPicksComponent;
  let fixture: ComponentFixture<ChoosePreviousPicksComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChoosePreviousPicksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChoosePreviousPicksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
