import React from 'react';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';

function PriceMenu() {
    return (
        <Typography align="left" paragraph={true}>
            <h1>Pricing</h1>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Grid container justify="center" spacing={2}>
                        <Grid item xs={4}>
                            <h2>Free</h2>
                            <p>
                                Have at it! Thanks for considering us.
                            </p>
                            <ul>
                                <li>Requests may be throttled.</li>
                                <li>Tell your friends!</li>
                            </ul>
                            <div class="price-call">
                                <h2 class="price">$0/mo.</h2>
                                <a href="mailto:trevor@ipsumllc.com">Contact Us</a>
                            </div>
                        </Grid>
                        <Grid item xs={4}>
                            <h2>Basic</h2>
                            <p>
                                Everything you need for your small team.
                            </p>
                            <ul>
                                <li>Preferred Service.</li>
                                <li>Access to Private Repos.</li>
                            </ul>
                            <div class="price-call">
                                <h2 class="price">$12.99/mo.</h2>
                                <a href="mailto:trevor@ipsumllc.com">Contact Us</a>
                            </div>
                        </Grid>
                        <Grid item xs={4}>
                            <h2>Enterprise</h2>
                            <p>
                                Enterprise solutions, including on-premise hosting, are available.&nbsp;
                            </p>
                            <ul>
                                <li>Unlimited Requests.</li>
                                <li>On-Premise Hosting.</li>
                            </ul>
                            <div class="price-call">
                                <h2 class="price">&nbsp;</h2>
                                <a href="mailto:trevor@ipsumllc.com">Contact Us</a>
                            </div>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Typography>
    )
}

export default PriceMenu;