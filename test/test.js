const chai = require('chai');
const chaiHttp = require('chai-http');
const app = "http://127.0.0.1:5000"; // change to ur localhost
chai.use(chaiHttp);
chai.should();

describe("Quotes API", () => {
    describe("GET /quotes", () => {
        it("should get all quotes", (done) => {
            chai.request(app)
                .get('/quotes')
                .end((err, res) => {
                    res.should.have.status(200);
                    res.body.should.be.a('array');
                    res.body.length.should.be.eql(2);
                    done();
                });
        });
    });

    describe("POST /quotes", () => {
        it("should create a new quote", (done) => {
            const newQuote = {
                text: "Test quote",
                author: "Test author"
            };
            chai.request(app)
                .post('/quotes')
                .send(newQuote)
                .end((err, res) => {
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('message').eql('Quote created successfully!');
                    res.body.quote.should.have.property('id').eql(3);
                    res.body.quote.should.have.property('text').eql('Test quote');
                    res.body.quote.should.have.property('author').eql('Test author');
                    done();
                });
        });
    });

    describe("PUT /quotes/:id", () => {
        it("should update an existing quote", (done) => {
            const updatedQuote = {
                id: 1,
                text: "Updated quote",
                author: "Updated author"
            };
            chai.request(app)
                .put('/quotes/1')
                .send(updatedQuote)
                .end((err, res) => {
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('message').eql('Quote updated successfully!');
                    res.body.quote.should.have.property('id').eql(1);
                    res.body.quote.should.have.property('text').eql('Updated quote');
                    res.body.quote.should.have.property('author').eql('Updated author');
                    done();
                });
        });
    });

    describe("DELETE /quotes/:id", () => {
        it("should delete an existing quote", (done) => {
            chai.request(app)
                .delete('/quotes/2')
                .end((err, res) => {
                    res.should.have.status(200);
                    res.body.should.be.a('object');
                    res.body.should.have.property('message').eql('Quote deleted successfully!');
                    done();
                });
        });
    });
});
