import random
import os
from faker import Faker

fake = Faker()

# Configuration
NUM_USERS = 25
NUM_LOCATIONS = 15
NUM_PLATFORMS = 3
NUM_ARTISTS = 12
NUM_LISTENERS = 40
NUM_RELEASES = 20
NUM_TRACKS = 50
NUM_STREAMS = 150

def generate_full_mysql_data():
    os.makedirs('dataset', exist_ok=True)

    user_roles = {}
    
    SCHEMA_PATH = 'database-files/00-audiovate.sql'

    with open('dataset/01_seed_data.sql', 'w') as f:
        # 1. Manually add the database creation
        f.write("CREATE DATABASE IF NOT EXISTS Audiovate;\n")
        f.write("USE Audiovate;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")

        f.write("DROP TABLE IF EXISTS `playlistEvent`, `streamEvent`, `track`, `release`, `artist`, `user`;\n\n")

        # 2. READ and WRITE the schema into this file
        f.write("-- START SCHEMA --\n")
        with open(SCHEMA_PATH, 'r') as schema_file:
            f.write(schema_file.read())
        f.write("\n-- END SCHEMA --\n\n")

        f.write("TRUNCATE TABLE user;\n")
        f.write("TRUNCATE TABLE artist;\n")
        f.write("TRUNCATE TABLE location;\n")
        f.write("TRUNCATE TABLE platform;\n")
        f.write("TRUNCATE TABLE systemLog;\n")
        f.write("TRUNCATE TABLE helpRequest;\n")
        f.write("TRUNCATE TABLE listener;\n")
        f.write("TRUNCATE TABLE playlist;\n")
        f.write("TRUNCATE TABLE `release`;\n")
        f.write("TRUNCATE TABLE manages;\n")
        f.write("TRUNCATE TABLE track;\n")
        f.write("TRUNCATE TABLE financialReport;\n")
        f.write("TRUNCATE TABLE asset;\n")
        f.write("TRUNCATE TABLE payoutProfiles;\n")
        f.write("TRUNCATE TABLE streamEvent;\n")
        f.write("TRUNCATE TABLE playlistEvent;\n")

        # 1. user
        f.write("-- 1. user\n")
        for i in range(1, NUM_USERS + 1):
            role = random.choice(['User', 'Admin', 'Data Analyst', 'Label Head'])
            user_roles[i] = role
            f.write(f"INSERT INTO `user` (user_id, first_name, last_name, role, email) VALUES "
                    f"({i}, '{fake.first_name()}', '{fake.last_name()}', '{role}', '{fake.unique.email()}');\n")
            
        eligible_artist_users = [uid for uid, role in user_roles.items() if role == 'User']
        eligible_managers = [uid for uid, role in user_roles.items() if role != 'Admin']

        # 2. location
        f.write("\n-- 2. location\n")
        for i in range(1, NUM_LOCATIONS + 1):
            country = fake.country().replace("'", "''")
            state = fake.state().replace("'", "''")
            city = fake.city().replace("'", "''")
            
            f.write(f"INSERT INTO location (location_id, country, region_state, city, postal_code, longitude, latitude) VALUES "
                    f"({i}, '{country}', '{state}', '{city}', "
                    f"{random.randint(1000, 9999)}, {random.randint(-180, 180)}, {random.randint(-90, 90)});\n")

        # 3. platform
        f.write("\n-- 3. platform\n")
        platforms = [("Spotify", 0.004), ("Apple Music", 0.01), ("Tidal", 0.012)]
        for i, (name, rev) in enumerate(platforms, 1):
            f.write(f"INSERT INTO platform (platform_id, name, estim_rev_per_unit) VALUES ({i}, '{name}', {rev});\n")

        # 4. artist
        actual_artist_ids = []
        f.write("\n-- 4. artist\n")
        num_to_create = min(NUM_ARTISTS, len(eligible_artist_users))
        for i in range(1, num_to_create + 1):
            user_id = eligible_artist_users[i-1]
            actual_artist_ids.append(i)
            f.write(f"INSERT INTO artist (artist_id, stage_name, bio, tax_id_status, artist_user_id) VALUES "
                    f"({i}, '{fake.user_name()}', '{fake.sentence()}', {random.randint(0,1)}, {i});\n")

        # 5. systemLog
        f.write("\n-- 5. systemLog\n")
        for i in range(1, 15):
            f.write(f"INSERT INTO systemLog (log_id, status, description, log_user_id, log_admin_id) VALUES "
                    f"({i}, {random.randint(0,1)}, '{fake.sentence()}', {random.randint(1,NUM_USERS)}, {random.randint(1,3)});\n")

        # 6. helpRequest
        f.write("\n-- 6. helpRequest\n")
        for i in range(1, 10):
            f.write(f"INSERT INTO helpRequest (request_id, submitted_user_id, status, description, assigned_admin_id) VALUES "
                    f"({i}, {random.randint(1,NUM_USERS)}, {random.randint(0,1)}, '{fake.sentence()}', {random.randint(1,3)});\n")

        # 7. listener
        f.write("\n-- 7. listener\n")
        for i in range(1, NUM_LISTENERS + 1):
            f.write(f"INSERT INTO listener (listener_id, age, gender, listener_location_id) VALUES "
                    f"({i}, {random.randint(13,80)}, '{random.choice(['F','M','NB','Other'])}', {random.randint(1,NUM_LOCATIONS)});\n")

        # 8. playlist
        f.write("\n-- 8. playlist\n")
        for i in range(1, 10):
            p_type = random.choice(['Editorial', 'Algorithm', 'User'])
            f.write(f"INSERT INTO playlist (playlist_id, name, type, p_platform_id) VALUES "
                    f"({i}, '{fake.word().capitalize()} Mix', '{p_type}', {random.randint(1,NUM_PLATFORMS)});\n")

        # 9. `release`
        f.write("\n-- 9. `release`\n")
        for i in range(1, NUM_RELEASES + 1):
            r_type = random.choice(['Album', 'Single', 'EP', 'Compilation'])
            r_status = random.choice(['Processing', 'Approved', 'Released', 'Takedown'])
            f.write(f"""INSERT INTO `release` (rel_id, title, type, status, release_date, release_artist_id) VALUES """
                f"""({i}, '{fake.catch_phrase().replace("'", "''")}', '{r_type}', '{r_status}', '{fake.date_time_this_year()}', {random.randint(1, NUM_ARTISTS)});\n""")

        # 10. manages (Relational table)
        f.write("\n-- 10. manages\n")
        f.write("-- Artists managing themselves\n")
        for a_id in actual_artist_ids:
            u_id = eligible_artist_users[a_id-1]
            f.write(f"INSERT INTO manages (manages_user_id, manages_artist_id) VALUES ({u_id}, {a_id});\n")
        
        f.write("-- Additional management assignments (No Admins)\n")
        for _ in range(15):
            m_uid = random.choice(eligible_managers)
            m_aid = random.choice(actual_artist_ids)
            f.write(f"INSERT IGNORE INTO manages (manages_user_id, manages_artist_id) VALUES ({m_uid}, {m_aid});\n")

        # 11. track
        f.write("\n-- 11. track\n")
        for i in range(1, NUM_TRACKS + 1):
            f.write(f"INSERT INTO track (track_id, title, genre, isrc_code, track_artist_id, track_release_id) VALUES "
                    f"""({i}, '{fake.bs().title().replace("'", "''")}', '{random.choice(['Lo-Fi', 'Rock', 'Pop'])}', """
                    f"'{fake.bothify('??##########').upper()}', {random.randint(1,NUM_ARTISTS)}, {random.randint(1,NUM_RELEASES)});\n")

        # 12. financialReport
        f.write("\n-- 12. financialReport\n")
        for i in range(1, 10):
            f.write(f"INSERT INTO financialReport (freport_id, start_period, end_period, fr_release_id) VALUES "
                    f"({i}, '2026-01-01 00:00:00', '2026-03-31 23:59:59', {random.randint(1,NUM_RELEASES)});\n")

        # 13. asset
        f.write("\n-- 13. asset\n")
        for i in range(1, NUM_RELEASES * 2):
            a_type = random.choice(['Audio','Artwork', 'Credits'])
            f.write(f"INSERT INTO asset (asset_id, file_url, file_type, upload_status, asset_release_id) VALUES "
                    f"({i}, '{fake.url()}', '{a_type}', 1, {random.randint(1,NUM_RELEASES)});\n")

        # 14. payoutProfiles
        f.write("\n-- 14. payoutProfiles\n")
        for i in range(1, NUM_RELEASES + 1):
            f.write(f"INSERT INTO payoutProfiles (payout_id, collab_email, role, split_percentage, pp_release_id) VALUES "
                    f"({i}, '{fake.email()}', 'Producer', 50.00, {i});\n")

        # 15. streamEvent
        f.write("\n-- 15. streamEvent\n")
        for i in range(1, NUM_STREAMS + 1):
            plat_idx = random.randint(0,2)
            rev = platforms[plat_idx][1]
            f.write(f"INSERT INTO streamEvent (event_id, time_stamp, is_skipped, rev_generated, event_listener_id, event_track_id, event_platform_id, event_location_id) VALUES "
                    f"({i}, '{fake.date_time_between('-30d','now')}', {random.randint(0,1)}, {rev}, {random.randint(1,NUM_LISTENERS)}, "
                    f"{random.randint(1,NUM_TRACKS)}, {plat_idx+1}, {random.randint(1,NUM_LOCATIONS)});\n")

        # 16. playlistEvent
        f.write("\n-- 16. playlistEvent\n")
        for i in range(1, 30):
            f.write(f"INSERT IGNORE INTO playlistEvent (pt_event_id, pt_playlist_id) VALUES ({random.randint(1,NUM_STREAMS)}, {random.randint(1,9)});\n")

        f.write("\nSET FOREIGN_KEY_CHECKS = 1;")

    print("Success: All 16 tables populated in dataset/seed_data.sql")

if __name__ == "__main__":
    generate_full_mysql_data()