import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ComparePicksComponent } from './compare-picks.component';

describe('ComparePicksComponent', () => {
  let component: ComparePicksComponent;
  let fixture: ComponentFixture<ComparePicksComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ComparePicksComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ComparePicksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
