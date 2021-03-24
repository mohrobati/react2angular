import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './App.component.ts';
import { EntryBoxComponent } from './Components/EntryBox/EntryBox.component.ts';
@NgModule({
	declarations: [
		AppComponent,
		EntryBoxComponent
    ],
    imports: [
        BrowserModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
        