function OnLinkedInFrameworkLoad() {
        IN.Event.on(IN, "auth", OnLinkedInAuth);
}

function OnLinkedInAuth() {
        IN.API.Profile("me").result(ShowProfileData);
}

function ShowProfileData(profiles) {
    var member = profiles.values[0];
    var id = member.id;
    var firstName = member.firstName;
    var lastName = member.lastName;
    var photo = member.pictureUrl;
    var headline = member.headline;

    //use information captured above
}
