module FirefoxHistory exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)

import Http

import String
import Json.Decode exposing (..)
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
    { debugBreadcrumb : String
    , rows : List (FirefoxHistoryRow)
    }


-- INIT


init : () -> ( Model, Cmd Msg )
init _ =
    -- The initial model comes from a Request, now it is hard coded
    ( Model
          "dummy debug"
          []
    , Cmd.batch [(httpRequestFirefoxHistory)]
    )



-- UPDATE


type Msg
    = Hello Int
    | ReceivedFirefoxHistory (Result Http.Error (List (FirefoxHistoryRow)))


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Hello a ->
            ( model

            , Cmd.none
            )

        ReceivedFirefoxHistory result ->
            case result of
                Ok status ->
                    ( {model | rows = status}, Cmd.none )

                Err e -> 
                    let
                      _ = Debug.log "error is " e
                    in
                      ( {model | rows = [FirefoxHistoryRow 1 "blahurl" (Just "blahtitle") (Just "blahdesc")]}, Cmd.none)

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW

renderFirefoxHistoryRow : FirefoxHistoryRow -> Html Msg
renderFirefoxHistoryRow row =
      tr []
          [
            td [id "hello"] [text "fucking elm parsing time"]
          , td [id "hello"] [text row.url]
          , td [id "hello"] [
                              (case row.title of
                                 Just a -> text a
                                 Nothing -> text "nothing"
                              )
                            ]
          ]
      
  
renderFirefoxHistoryTable : List (FirefoxHistoryRow) -> Html Msg
renderFirefoxHistoryTable rows = 
    table [class "table"]
      [
        tbody [] 
          (List.map renderFirefoxHistoryRow rows)
      ]


    

view : Model -> Html Msg
view model =
    div [id "container"] 
    (List.append
      [ h2 [] [text "Firefox History"]
      ]
      
      [(renderFirefoxHistoryTable model.rows)
      ]
    )



-- HTTP

httpRequestFirefoxHistory : Cmd Msg
httpRequestFirefoxHistory =
    Http.post
        { body =
            (Http.stringBody "hello" "wtf")
        , url = "http://localhost:9999/api/firefoxhistory"
        , expect = Http.expectJson ReceivedFirefoxHistory firefoxHistoryDecoder
        }


type alias FirefoxHistoryRow = 
  { last_visit_date : Int
  , url : String
  , title : Maybe String
  , description: Maybe String
  }

firefoxHistoryDecoder : Decoder (List FirefoxHistoryRow)
firefoxHistoryDecoder =
    Json.Decode.list (firefoxHistoryRowDecoder)

firefoxHistoryRowDecoder : Decoder FirefoxHistoryRow
firefoxHistoryRowDecoder =
    map4 FirefoxHistoryRow
        (field "last_visit_date" int)
        (field "url" string)
        (maybe <| field "title" string)
        (maybe <| field "description" string)
