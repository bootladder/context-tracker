module LocalSystemStatus exposing (..)

import Browser
import Date
import Debug exposing (toString)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http
import Json.Decode exposing (..)
import String exposing (..)
import Task exposing (perform)
import Time exposing (..)



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
    { ramusagegigs : Float
    }



-- INIT



init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
    3.2
    , Cmd.batch [  ]
    )



-- UPDATE


type Msg
    = Hello Int


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello a ->
            ( model
            , Cmd.none
            )





-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


renderRAMUsage : Float -> Html Msg
renderRAMUsage ramusage =
    div []
    [ span [] [text "RAM Usage: "]
        , span [] [text <| toString ramusage]
    , span [] []
    , span [] [text "%"]
    ]


view : Model -> Html Msg
view model =
    div
        [ id "local-system-status-container"
        , class "bg-light"
        ]
        [ div [] [text "blah system"]
        , renderRAMUsage model.ramusagegigs
        , renderRAMUsage model.ramusagegigs
        ]
