import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CompareRecordsComponent } from './compare-records.component';

describe('CompareRecordsComponent', () => {
  let component: CompareRecordsComponent;
  let fixture: ComponentFixture<CompareRecordsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CompareRecordsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CompareRecordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
