// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,
  firebase: {
    apiKey: "AIzaSyCSJ-jAkye3uTC2T9DfjhlsL1Hz_78V9sE",
    authDomain: "nfl-picks-b5e4d.firebaseapp.com",
    databaseURL: "https://nfl-picks-b5e4d.firebaseio.com",
    projectId: "nfl-picks-b5e4d",
    storageBucket: "nfl-picks-b5e4d.appspot.com",
    messagingSenderId: "348465044323"
  }
};
