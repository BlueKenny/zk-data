//import QtQuick 2.2
//import QtQuick.Controls 1.1
//import QtQuick.Layouts 1.1

import Ubuntu.Components 1.3
import Ubuntu.Unity.Action 1.1 as UnityActions
import UserMetrics 0.1
import Ubuntu.Content 1.3
import CameraApp 0.1

ApplicationWindow{
    visible:true
    width:640
    height:480
    id:window
    title: "editor"

    //signal textUpdated(string text)
	Camera.CaptureStillImage

    TextArea{
        text:"hello"
        //onTextChanged: textUpdated(text);
    }

}
