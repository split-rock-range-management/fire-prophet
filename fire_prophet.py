# fire_prophet.py

def calculate_ros(model_type, wind_speed, slope_percent, moisture_percent):
    f_w = min(wind_speed / 30, 1.0)
    f_s = min(slope_percent / 45, 1.0)
    f_m = 1.0 - min(moisture_percent / 30, 1.0)

    weights = {
        "balanced":       (0.4, 0.4, 0.2),
        "wind_dominant":  (0.6, 0.3, 0.1),
        "slope_dominant": (0.3, 0.6, 0.1)
    }

    if model_type not in weights:
        raise ValueError(f"Invalid model type: {model_type}")

    a_w, a_s, a_m = weights[model_type]
    B = 0.1  # baseline RoS in m/min
    ros = B * (1 + a_w * f_w + a_s * f_s + a_m * f_m)
    return ros


def calculate_intensity_and_flame_length(ros, fuel_load=1.2, heat_content=18000):
    intensity = heat_content * fuel_load * ros
    flame_length = 0.45 * (intensity ** 0.46)
    return intensity, flame_length


def calculate_species_resilience(
    bark_thickness=0.5,
    resprouting_ability=0.5,
    crown_height=0.5,
    moisture_content=0.5,
    seed_dependency=0.5
):
    positive_traits = (
        0.3 * bark_thickness +
        0.25 * resprouting_ability +
        0.2 * crown_height +
        0.15 * moisture_content
    )
    penalty = 0.2 * seed_dependency
    resilience = 1.0 + positive_traits - penalty
    return round(resilience, 2)


def estimate_survival(flame_length, species_resilience):
    lethal_threshold = 2.0 * species_resilience
    survival = max(0.0, 1.0 - (flame_length / lethal_threshold))
    return round(survival * 100, 1)


def fire_prophet(model_type, wind_speed, slope_percent, moisture_percent, traits):
    ros = calculate_ros(model_type, wind_speed, slope_percent, moisture_percent)
    intensity, flame_length = calculate_intensity_and_flame_length(ros)
    resilience = calculate_species_resilience(**traits)
    survival = estimate_survival(flame_length, resilience)

    return {
        "model": model_type,
        "rate_of_spread_m_per_min": round(ros, 2),
        "intensity_kw_per_m": round(intensity, 0),
        "flame_length_m": round(flame_length, 2),
        "species_resilience": resilience,
        "survival_probability_percent": survival
    }


def batch_process_species_assemblage(model_type, wind_speed, slope_percent, moisture_percent, assemblage):
    results = {}
    for species_name, traits in assemblage.items():
        results[species_name] = fire_prophet(
            model_type,
            wind_speed,
            slope_percent,
            moisture_percent,
            traits
        )
    return results