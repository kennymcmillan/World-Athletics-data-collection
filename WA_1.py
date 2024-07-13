import asyncio
import nest_asyncio
import pandas as pd
import worldathletics
from worldathletics import GetCalendarCompetitionResults

nest_asyncio.apply()

client = worldathletics.WorldAthletics()

async def main():
    offset = 0
    limit = 100
    competition_data = []

    while offset < limit:
        try:
            response = await client.get_calendar_events(
                hide_competitions_with_no_results=True,
                limit=limit,
                region_type='world',
                offset=offset,
                show_options_with_no_hits=False,
                order_direction='Ascending',
                competition_group_id=None,
                competition_subgroup_id=None,
                discipline_id=None,
                end_date=None,
                permit_level_id=None,
                query=None,
                ranking_category_id=None,
                region_id=None,
                start_date=None,
            )

            # Assuming response is a list of tuples
            for key, event_data in response:
                if key == 'get_calendar_events' and event_data.results:
                    for event in event_data.results:
                        try:
                            competition_info = {
                                "Competition ID": event.id,
                                "Name": event.name,
                                "Venue": event.venue,
                                "Date Range": event.date_range
                            }

                            # Fetching competition results for each event
                            competition_response = await client.get_calendar_competition_results(competition_id=event.id)
                            
                            if competition_response.get_calendar_competition_results:
                                competition = competition_response.get_calendar_competition_results.competition
                                event_titles = competition_response.get_calendar_competition_results.event_titles
                                
                                for event_title in event_titles:
                                    for ev in event_title.events:
                                        for race in ev.races:
                                            for result in race.results:
                                                result_info = {
                                                    "Event Title": event_title.event_title,
                                                    "Event": ev.event,
                                                    "Race": race.race,
                                                    "Competitor Name": result.competitor.name,
                                                    "IAAF ID": result.competitor.iaaf_id,
                                                    "Mark": result.mark,
                                                    "Wind": result.wind,
                                                    "Nationality": result.nationality,
                                                    "Place": result.place,
                                                    "Points": result.points,
                                                    "Qualified": result.qualified,
                                                    "Records": result.records,
                                                    "Remark": result.remark
                                                }
                                                # Merge competition info with result info
                                                competition_data.append({**competition_info, **result_info})
                        except Exception as e:
                            print(f"Error processing competition {event.id}: {e}")
                            continue

            if len(event_data.results) < limit:
                break
            offset += limit

        except Exception as e:
            print(f"Error fetching data: {e}")
            continue

    # Create a DataFrame from the competition data
    df = pd.DataFrame(competition_data)
    df.to_csv('competition_data.csv', index=False, encoding='utf-16')

if __name__ == '__main__':
    asyncio.run(main())
