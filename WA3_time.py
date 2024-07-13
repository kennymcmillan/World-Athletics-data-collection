import asyncio
import nest_asyncio
import pandas as pd
import polars as pl
import worldathletics
from worldathletics import GetCalendarCompetitionResults
import random
import time

nest_asyncio.apply()

client = worldathletics.WorldAthletics()

async def main():
    start_time = time.time()  # Record the start time

    limit = 17000
    batch_size = 100
    competition_data = []

    for offset in range(0, limit, batch_size):
        try:
            response = await client.get_calendar_events(
                hide_competitions_with_no_results=True,
                limit=batch_size,
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

            print(f"Batch from offset {offset} to {offset + batch_size} completed.")

            # Introduce a random pause between batches
            pause_duration = random.uniform(5, 10)
            print(f"Pausing for {pause_duration:.2f} seconds to avoid rate limiting...")
            time.sleep(pause_duration)

        except Exception as e:
            print(f"Error fetching data: {e}")
            continue

    # Create a DataFrame from the competition data
    df = pd.DataFrame(competition_data)
    df.to_parquet('competition_data.parquet')

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"All batches completed. Data has been saved to 'competition_data.parquet'.")
    print(f"Total time taken for scraping: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    asyncio.run(main())

df = pl.read_parquet('competition_data.parquet')
