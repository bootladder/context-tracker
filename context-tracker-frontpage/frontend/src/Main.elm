module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

import Http

import String


-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type alias Model =
    { debugBreadcrumb : String
    , gitStatus : String
    }


-- INIT


init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
          "dummy debug"
          "dummy status"
    , Cmd.batch [(httpRequestGitStatus)]
    )



-- UPDATE


type Msg
    = Hello Int
    | ReceivedGitStatus (Result Http.Error (String))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello a ->
            ( model

            , Cmd.none
            )

        ReceivedGitStatus result ->
            case result of
                Ok status ->
                    ( {model | gitStatus = status}, Cmd.none )
                Err e -> (model, Cmd.none)

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    div [id "container"] 
    [ h2 [] [text "Context Viewer of"]
    , div [] [text model.gitStatus]
    , div [] [text "filesystem events"]
    , div [] [text "shell commands"]
    ]



-- HTTP

httpRequestGitStatus : Cmd Msg
httpRequestGitStatus =
    Http.post
        { body =
            (Http.stringBody "hello" "wtf")
        , url = "http://localhost:9090/api/"
        , expect = Http.expectString ReceivedGitStatus
        }
