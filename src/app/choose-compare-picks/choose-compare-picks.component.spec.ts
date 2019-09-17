import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChooseComparePicksComponent } from './choose-compare-picks.component';

describe('ChooseComparePicksComponent', () => {
  let component: ChooseComparePicksComponent;
  let fixture: ComponentFixture<ChooseComparePicksComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChooseComparePicksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChooseComparePicksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
