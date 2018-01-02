import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PreviousPicksComponent } from './previous-picks.component';

describe('PreviousPicksComponent', () => {
  let component: PreviousPicksComponent;
  let fixture: ComponentFixture<PreviousPicksComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PreviousPicksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PreviousPicksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
